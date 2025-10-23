import {
  Alert,
  AlertDescription,
  AlertIcon,
  AlertTitle,
  Box,
  HStack,
  Skeleton,
  Stack,
  Tag,
  Text,
} from "@chakra-ui/react";

import type { ChatMessage } from "../types";

interface ChatThreadProps {
  messages: ChatMessage[];
  isLoading: boolean;
  error?: string;
}

const renderSources = (sources: ChatMessage["sources"]) => {
  if (!sources || sources.length === 0) {
    return null;
  }

  return (
    <HStack spacing={2} mt={2} flexWrap="wrap">
      {sources.map((source) => (
        <Tag key={source.document_id} colorScheme="purple" size="sm">
          {source.document_id}
        </Tag>
      ))}
    </HStack>
  );
};

export const ChatThread = ({ messages, isLoading, error }: ChatThreadProps) => {
  return (
    <Stack spacing={4} maxH="60vh" overflowY="auto" pr={4}>
      {error ? (
        <Alert status="error" borderRadius="md">
          <AlertIcon />
          <AlertTitle>Something went wrong.</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      ) : null}

      {messages.map((message) => (
        <Box
          key={message.id}
          alignSelf={message.role === "user" ? "flex-end" : "flex-start"}
          bg={message.role === "user" ? "blue.500" : "gray.100"}
          color={message.role === "user" ? "white" : "gray.800"}
          px={4}
          py={3}
          borderRadius="xl"
          maxW="75%"
        >
          <Text whiteSpace="pre-wrap">{message.content}</Text>
          {renderSources(message.sources)}
        </Box>
      ))}

      {isLoading ? (
        <Stack spacing={2} maxW="50%">
          <Skeleton height="20px" />
          <Skeleton height="20px" />
        </Stack>
      ) : null}

      {!messages.length && !isLoading ? (
        <Box textAlign="center" color="gray.500">
          <Text>Start the conversation by asking about CI&T Flow APIs.</Text>
        </Box>
      ) : null}
    </Stack>
  );
};
