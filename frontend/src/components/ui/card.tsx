import { cn } from '@/lib/utils'
import * as React from 'react'

function Card({ className, ...props }: React.ComponentProps<'div'>) {
  return (
    <div
      data-slot="card"
      className={cn('border border-gray-200 bg-card text-card-foreground flex flex-col gap-6 rounded-md shadow-sm', className)}
      {...props}
    />
  )
}

function CardHeader({ className, ...props }: React.ComponentProps<'div'>) {
  return (
    <div
      data-slot="card-header"
      className={cn(
        '@container/card-header grid auto-rows-min grid-rows-[auto_auto] items-start gap-1.5 px-6 has-[data-slot=card-action]:grid-cols-[1fr_auto] [.border-b]:pb-6',
        className,
      )}
      {...props}
    />
  )
}

type CardTitleProps = {
  title?: React.ReactNode;
  subtitle?: React.ReactNode;
  date?: React.ReactNode;
} & React.ComponentProps<'div'>;

function CardTitle({ className, title, subtitle, date, ...props }: CardTitleProps) {
  return (
    <div data-slot="card-title" className={cn('leading-none font-semibold space-y-2 mt-4', className)} {...props}>
      <div className="text-lg font-bold line-clamp-1 mb-2">{title}</div>
      <div className="text-sm text-gray-600 line-clamp-1 mb-1">
        <span className="font-medium">S/N:</span> {subtitle}
      </div>
      <div className="text-sm text-gray-600 line-clamp-1">
        <span className="font-medium">구매일:</span> {date}
      </div>
    </div>
  )
}

function CardDescription({ className, ...props }: React.ComponentProps<'div'>) {
  return <div data-slot="card-description" className={cn('text-muted-foreground text-sm', className)} {...props} />
}

function CardAction({ className, ...props }: React.ComponentProps<'div'>) {
  return (
    <div
      data-slot="card-action"
      className={cn('col-start-2 row-span-2 row-start-1 self-start justify-self-end', className)}
      {...props}
    />
  )
}

function CardContent({ className, ...props }: React.ComponentProps<'div'>) {
  return <div data-slot="card-content" className={cn('px-6', className)} {...props} />
}

function CardFooter({ className, ...props }: React.ComponentProps<'div'>) {
  return <div data-slot="card-footer" className={cn('flex items-center px-6 [.border-t]:pt-6', className)} {...props} />
}

export { Card, CardHeader, CardFooter, CardTitle, CardAction, CardDescription, CardContent }
