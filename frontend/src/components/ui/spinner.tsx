interface SpinnerProps {
  size?: "sm" | "md" | "lg";
  className?: string;
}

const sizeClasses = {
  sm: "h-4 w-4",
  md: "h-6 w-6",
  lg: "h-10 w-10",
};

export function Spinner({ size = "md", className = "" }: SpinnerProps) {
  return (
    <div className={`${sizeClasses[size]} ${className}`} role="status">
      <svg className="h-full w-full animate-spin text-primary-600" viewBox="0 0 24 24" fill="none">
        <circle className="opacity-20" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" />
        <path className="opacity-80" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
      </svg>
      <span className="sr-only">Loading...</span>
    </div>
  );
}

export function FullPageSpinner({ text }: { text?: string }) {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-4">
      <Spinner size="lg" />
      {text && <p className="text-sm font-medium text-text-tertiary">{text}</p>}
    </div>
  );
}

export function SectionSpinner({ text }: { text?: string }) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 py-16">
      <Spinner size="md" />
      {text && <p className="text-sm text-text-tertiary">{text}</p>}
    </div>
  );
}
