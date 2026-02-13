import { Alert } from "@/components/ui/alert";

interface DisclaimerBannerProps {
  text?: string;
}

export function DisclaimerBanner({ text }: DisclaimerBannerProps) {
  return (
    <Alert variant="warning">
      <strong>Herramienta informativa.</strong>{" "}
      {text ||
        "Los resultados son orientativos con base en la información proporcionada y no reemplazan el consejo de un profesional tributario."}
    </Alert>
  );
}
