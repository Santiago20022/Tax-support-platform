import { type HTMLAttributes } from "react";

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  padding?: boolean;
  hover?: boolean;
}

export function Card({
  padding = true,
  hover = false,
  className = "",
  children,
  ...props
}: CardProps) {
  return (
    <div
      className={`rounded-2xl border border-gray-100 bg-white shadow-sm ${
        hover ? "transition-all duration-200 hover:-translate-y-0.5 hover:shadow-md hover:border-gray-200" : ""
      } ${padding ? "p-6" : ""} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardHeader({
  className = "",
  children,
}: {
  className?: string;
  children: React.ReactNode;
}) {
  return <div className={`mb-4 ${className}`}>{children}</div>;
}

export function CardTitle({
  className = "",
  children,
}: {
  className?: string;
  children: React.ReactNode;
}) {
  return (
    <h3 className={`text-lg font-semibold tracking-tight text-gray-900 ${className}`}>
      {children}
    </h3>
  );
}
