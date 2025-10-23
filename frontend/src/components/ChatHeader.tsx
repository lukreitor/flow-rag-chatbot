import { Box, Heading, HStack, IconButton, Text, Tooltip, useToast } from "@chakra-ui/react";
import { RepeatIcon } from "@chakra-ui/icons";

interface ChatHeaderProps {
  onReset: () => void;
}

export const ChatHeader = ({ onReset }: ChatHeaderProps) => {
  const toast = useToast();

  const handleReset = () => {
    onReset();
    toast({ title: "Conversation cleared", status: "info", duration: 2000 });
  };

  return (
    <HStack justify="space-between" align="center">
      <Box>
        <Heading size="lg">Flow RAG Chatbot</Heading>
        <Text color="gray.600">Ask questions about CI&T Flow APIs with document grounded answers.</Text>
      </Box>
      <Tooltip label="Reset conversation">
        <IconButton aria-label="Reset conversation" icon={<RepeatIcon />} onClick={handleReset} />
      </Tooltip>
    </HStack>
  );
};
