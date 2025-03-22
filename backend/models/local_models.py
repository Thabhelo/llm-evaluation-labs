from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModel
import torch
from typing import Dict, Optional, List
from pathlib import Path
import logging
from ..config import settings

logger = logging.getLogger(__name__)

class LocalModelManager:
    def __init__(self):
        self.models: Dict[str, AutoModel] = {}
        self.tokenizers: Dict[str, AutoTokenizer] = {}
        self.model_path = Path(settings.LOCAL_MODELS_PATH)
        self.model_path.mkdir(parents=True, exist_ok=True)
        
        # Efficient, free models suitable for evaluation
        self.default_models = [
            "TinyLlama/TinyLlama-1.1B-Chat-v1.0",  # Efficient chat model
            "facebook/opt-350m",  # Small general model
            "microsoft/phi-2",  # Efficient reasoning model
            "MBZUAI/LaMini-GPT-1.5B",  # Lightweight GPT
            "google/flan-t5-small",  # Small instruction model
        ]

    async def load_model(self, model_name: str) -> bool:
        """Load a model and its tokenizer."""
        try:
            if model_name in self.models:
                return True

            if len(self.models) >= settings.MAX_LOCAL_MODELS:
                self._unload_lru_model()

            logger.info(f"Loading model: {model_name}")
            
            # Load tokenizer
            tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                cache_dir=str(self.model_path),
                trust_remote_code=True
            )

            # Load model with optimizations
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                cache_dir=str(self.model_path),
                torch_dtype=torch.float16,  # Use half precision
                low_cpu_mem_usage=True,  # Optimize CPU memory
                device_map="auto",  # Auto device placement
                trust_remote_code=True
            )

            # Basic model optimization
            model.eval()  # Set to evaluation mode
            if torch.cuda.is_available():
                model = model.cuda()  # Move to GPU if available

            self.models[model_name] = model
            self.tokenizers[model_name] = tokenizer
            return True

        except Exception as e:
            logger.error(f"Error loading model {model_name}: {e}")
            return False

    def _unload_lru_model(self) -> None:
        """Unload the least recently used model."""
        if self.models:
            lru_model = next(iter(self.models))
            del self.models[lru_model]
            del self.tokenizers[lru_model]
            torch.cuda.empty_cache()
            logger.info(f"Unloaded model: {lru_model}")

    async def get_available_models(self) -> List[str]:
        """Get list of available local models."""
        try:
            # Check for downloaded models
            downloaded = [
                p.name for p in self.model_path.glob("*")
                if p.is_dir() and not p.name.startswith(".")
            ]
            
            # Return downloaded models or defaults
            return downloaded if downloaded else self.default_models
        except Exception as e:
            logger.error(f"Error getting available models: {e}")
            return self.default_models

    async def generate(
        self,
        model_name: str,
        prompt: str,
        max_length: int = 100,
        temperature: float = 0.7,
        top_p: float = 0.9,
        num_return_sequences: int = 1,
    ) -> Optional[str]:
        """Generate text using a local model."""
        try:
            if not await self.load_model(model_name):
                return None

            model = self.models[model_name]
            tokenizer = self.tokenizers[model_name]

            # Prepare input
            inputs = tokenizer(
                prompt,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512  # Reasonable input length limit
            ).to(model.device)
            
            # Generate with memory optimization
            with torch.no_grad(), torch.cuda.amp.autocast():
                outputs = model.generate(
                    **inputs,
                    max_length=max_length,
                    temperature=temperature,
                    top_p=top_p,
                    num_return_sequences=num_return_sequences,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id,
                    early_stopping=True
                )
            
            # Decode and return
            return tokenizer.decode(outputs[0], skip_special_tokens=True)

        except Exception as e:
            logger.error(f"Error generating text with model {model_name}: {e}")
            return None

# Global instance
model_manager = LocalModelManager() 