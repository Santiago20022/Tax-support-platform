import { type InputHTMLAttributes, forwardRef } from "react";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  hint?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  function Input({ label, error, hint, id, className = "", ...props }, ref) {
    return (
      <div className="w-full">
        {label && (
          <label
            htmlFor={id}
            className="mb-1.5 block text-sm font-medium text-text-label"
          >
            {label}
          </label>
        )}
        <input
          ref={ref}
          id={id}
          className={`block w-full rounded-xl border bg-input-bg px-4 py-2.5 text-sm text-text-primary shadow-sm transition-all duration-200 placeholder:text-text-tertiary hover:border-text-tertiary focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20 disabled:bg-surface-secondary disabled:text-text-tertiary ${
            error
              ? "border-danger-500 hover:border-danger-500 focus:border-danger-500 focus:ring-danger-500/20"
              : "border-border-strong"
          } ${className}`}
          {...props}
        />
        {error && <p className="mt-1.5 text-xs font-medium text-danger-600">{error}</p>}
        {hint && !error && <p className="mt-1.5 text-xs text-text-tertiary">{hint}</p>}
      </div>
    );
  },
);
