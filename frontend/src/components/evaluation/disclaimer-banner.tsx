import { Alert } from "@/components/ui/alert";
import { useT } from "@/lib/language-context";

interface DisclaimerBannerProps {
  text?: string;
}

export function DisclaimerBanner({ text }: DisclaimerBannerProps) {
  const t = useT();

  return (
    <Alert variant="warning">
      <strong>{t.disclaimer.title}</strong>{" "}
      {text || t.disclaimer.defaultText}
    </Alert>
  );
}
