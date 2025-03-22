import { HTMLAttributes, TdHTMLAttributes, ThHTMLAttributes } from 'react'

const Table = ({ className = '', ...props }: HTMLAttributes<HTMLTableElement>) => (
  <div className="relative w-full overflow-auto">
    <table
      className={`w-full caption-bottom text-sm ${className}`}
      {...props}
    />
  </div>
)

const TableHeader = ({
  className = '',
  ...props
}: HTMLAttributes<HTMLTableSectionElement>) => (
  <thead className={`bg-muted/50 ${className}`} {...props} />
)

const TableBody = ({
  className = '',
  ...props
}: HTMLAttributes<HTMLTableSectionElement>) => (
  <tbody className={`[&_tr:last-child]:border-0 ${className}`} {...props} />
)

const TableFooter = ({
  className = '',
  ...props
}: HTMLAttributes<HTMLTableSectionElement>) => (
  <tfoot
    className={`border-t bg-muted/50 font-medium [&>tr]:last:border-b-0 ${className}`}
    {...props}
  />
)

const TableRow = ({
  className = '',
  ...props
}: HTMLAttributes<HTMLTableRowElement>) => (
  <tr
    className={`border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted ${className}`}
    {...props}
  />
)

const TableHead = ({
  className = '',
  ...props
}: ThHTMLAttributes<HTMLTableCellElement>) => (
  <th
    className={`h-12 px-4 text-left align-middle font-medium text-muted-foreground [&:has([role=checkbox])]:pr-0 ${className}`}
    {...props}
  />
)

const TableCell = ({
  className = '',
  ...props
}: TdHTMLAttributes<HTMLTableCellElement>) => (
  <td
    className={`p-4 align-middle [&:has([role=checkbox])]:pr-0 ${className}`}
    {...props}
  />
)

const TableCaption = ({
  className = '',
  ...props
}: HTMLAttributes<HTMLTableCaptionElement>) => (
  <caption
    className={`mt-4 text-sm text-muted-foreground ${className}`}
    {...props}
  />
)

export {
  Table,
  TableHeader,
  TableBody,
  TableFooter,
  TableHead,
  TableRow,
  TableCell,
  TableCaption,
} 