import { AddIcon } from '@chakra-ui/icons';
import { Box, Button, Flex, Heading, Spinner, Stack, Text, VStack } from '@chakra-ui/react';

import type { ConversationSummary } from '../types';

interface ConversationSidebarProps {
  conversations: ConversationSummary[];
  activeConversationId?: string;
  onSelect: (conversationId: string) => void;
  onNewChat: () => void;
  isLoading: boolean;
  isDisabled: boolean;
  nickname?: string | null;
  errorMessage?: string;
}

const getConversationLabel = (conversation: ConversationSummary): string => {
  const base = conversation.title?.trim() || conversation.last_message_preview?.trim();
  return base && base.length > 0 ? base : 'New chat';
};

export const ConversationSidebar = ({
  conversations,
  activeConversationId,
  onSelect,
  onNewChat,
  isLoading,
  isDisabled,
  nickname,
  errorMessage,
}: ConversationSidebarProps) => {
  return (
    <Flex direction="column" h="100%" bg="gray.900" color="gray.100" px={4} py={6} gap={6}>
      <Box>
        <Heading size="md">Chats</Heading>
        <Text fontSize="sm" color="gray.400">
          {nickname ? `Signed in as ${nickname}` : 'Set a nickname to get started'}
        </Text>
      </Box>
      <Button
        leftIcon={<AddIcon />}
        onClick={onNewChat}
        isDisabled={isDisabled}
        colorScheme="teal"
        variant="solid"
      >
        Start new chat
      </Button>
      <Box flex="1" overflowY="auto">
        {errorMessage ? (
          <Text fontSize="sm" color="red.300">
            {errorMessage}
          </Text>
        ) : isLoading ? (
          <Flex align="center" justify="center" h="full">
            <Spinner color="gray.300" />
          </Flex>
        ) : conversations.length === 0 ? (
          <Text fontSize="sm" color="gray.400">
            {isDisabled ? 'Your future chats will appear here' : 'No conversations yet.'}
          </Text>
        ) : (
          <VStack align="stretch" spacing={2}>
            {conversations.map((conversation) => {
              const isActive = activeConversationId === conversation.id;
              return (
                <Button
                  key={conversation.id}
                  justifyContent="flex-start"
                  variant="ghost"
                  onClick={() => onSelect(conversation.id)}
                  isDisabled={isDisabled}
                  bg={isActive ? 'whiteAlpha.200' : 'transparent'}
                  _hover={{ bg: 'whiteAlpha.200' }}
                  _active={{ bg: 'whiteAlpha.300' }}
                  h="auto"
                  py={3}
                  whiteSpace="normal"
                  textAlign="left"
                >
                  <Stack spacing={1} align="stretch">
                    <Text fontWeight="semibold" noOfLines={1}>
                      {getConversationLabel(conversation)}
                    </Text>
                    <Text fontSize="xs" color="gray.400" noOfLines={1}>
                      Updated {new Date(conversation.updated_at).toLocaleString()}
                    </Text>
                  </Stack>
                </Button>
              );
            })}
          </VStack>
        )}
      </Box>
    </Flex>
  );
};
