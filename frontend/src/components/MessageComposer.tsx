import { ArrowForwardIcon } from "@chakra-ui/icons";
import { Button, HStack, Input, useToast } from "@chakra-ui/react";
import { ChangeEvent, FormEvent, useState } from "react";

interface MessageComposerProps {
  onSend: (message: string) => void;
  isLoading: boolean;
  isDisabled?: boolean;
}

export const MessageComposer = ({ onSend, isLoading, isDisabled = false }: MessageComposerProps) => {
  const [message, setMessage] = useState("");
  const toast = useToast();

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (isDisabled) {
      return;
    }
    if (!message.trim()) {
      toast({ title: "Please enter a message", status: "warning", duration: 2000 });
      return;
    }
    onSend(message.trim());
    setMessage("");
  };

  return (
    <form onSubmit={handleSubmit}>
      <HStack spacing={3}>
        <Input
          value={message}
          onChange={(event: ChangeEvent<HTMLInputElement>) => setMessage(event.target.value)}
          placeholder="Ask anything about Flow"
          isDisabled={isLoading || isDisabled}
        />
        <Button
          type="submit"
          rightIcon={<ArrowForwardIcon />}
          isLoading={isLoading}
          colorScheme="blue"
          isDisabled={isDisabled}
        >
          Send
        </Button>
      </HStack>
    </form>
  );
};
