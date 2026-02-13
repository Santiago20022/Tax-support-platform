interface BadgeProps {
  children: React.ReactNode;
  variant?: "success" | "danger" | "warning" | "info" | "gray";
  size?: "sm" | "md";
  dot?: boolean;
  className?: string;
}

const variantClasses = {
  success: "bg-success-50 text-success-700 ring-success-600/10",
  danger: "bg-danger-50 text-danger-700 ring-danger-600/10",
  warning: "bg-warning-50 text-warning-700 ring-warning-600/10",
  info: "bg-primary-50 text-primary-700 ring-primary-600/10",
  gray: "bg-gray-50 text-gray-600 ring-gray-500/10",
};

const dotColors = {
  success: "bg-success-500",
  danger: "bg-danger-500",
  warning: "bg-warning-500",
  info: "bg-primary-500",
  gray: "bg-gray-400",
};

const sizeClasses = {
  sm: "px-2 py-0.5 text-[10px]",
  md: "px-2.5 py-1 text-xs",
};

export function Badge({
  children,
  variant = "gray",
  size = "md",
  dot = false,
  className = "",
}: BadgeProps) {
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-lg font-semibold ring-1 ring-inset ${variantClasses[variant]} ${sizeClasses[size]} ${className}`}
    >
      {dot && (
        <span className={`h-1.5 w-1.5 rounded-full ${dotColors[variant]}`} />
      )}
      {children}
    </span>
  );
}
