import { AddIcon } from '@chakra-ui/icons';
import { Box, Button, Container, Flex, Heading, HStack, Stack, Text } from '@chakra-ui/react';
import { useQuery } from '@tanstack/react-query';
import { useState } from 'react';

import { ConversationSidebar } from '../components/ConversationSidebar';
import { ChatThread } from '../components/ChatThread';
import { DocumentUploader } from '../components/DocumentUploader';
import { MessageComposer } from '../components/MessageComposer';
import { NicknameGate } from '../components/NicknameGate';
import { useChat } from '../hooks/useChat';
import { api } from '../lib/api';
import type { ConversationSummary } from '../types';

const App = () => {
  const [nickname, setNickname] = useState<string | null>(() => {
    if (typeof window === 'undefined') {
      return null;
    }
    return window.localStorage.getItem('flow-nickname');
  });
  const {
    conversationId,
    messages,
    sendMessage,
    selectConversation,
    startNewConversation,
    isSending,
    isHistoryLoading,
    error,
  } = useChat(nickname);
  const isAuthenticated = Boolean(nickname);
  const {
    data: conversationData,
    isFetching: isFetchingConversations,
    isError: isConversationsError,
    error: conversationsError,
  } = useQuery<ConversationSummary[], Error>({
    queryKey: ['conversations', nickname],
    queryFn: async () => {
      const response = await api.get<ConversationSummary[]>('/conversations', {
        params: { nickname },
      });
      return response.data;
    },
    enabled: isAuthenticated,
    staleTime: 30_000,
  });

  const conversations = isAuthenticated ? (conversationData ?? []) : [];
  const conversationErrorMessage = isConversationsError
    ? (conversationsError?.message ?? 'Unable to load conversations.')
    : undefined;
  const combinedLoading = isSending || isHistoryLoading;

  return (
    <Flex minH="100vh" bg="gray.900" direction={{ base: 'column', md: 'row' }}>
      <Box w={{ base: '100%', md: '300px' }}>
        <ConversationSidebar
          conversations={conversations}
          activeConversationId={conversationId}
          onSelect={selectConversation}
          onNewChat={startNewConversation}
          isLoading={isFetchingConversations}
          isDisabled={!isAuthenticated}
          nickname={nickname}
          errorMessage={conversationErrorMessage}
        />
      </Box>
      <Flex direction="column" flex="1" bg="gray.50">
        <Box as="header" borderBottomWidth="1px" borderColor="gray.200" bg="white" px={6} py={4}>
          <Container maxW="5xl">
            <HStack justify="space-between" align="center">
              <Box>
                <Heading size="md">Flow RAG Chatbot</Heading>
                <Text fontSize="sm" color="gray.500">
                  Document-grounded answers for CI&T Flow APIs.
                </Text>
              </Box>
              <Button
                leftIcon={<AddIcon />}
                onClick={startNewConversation}
                colorScheme="teal"
                isDisabled={!isAuthenticated}
              >
                New chat
              </Button>
            </HStack>
          </Container>
        </Box>
        <Flex direction="column" flex="1" overflow="hidden">
          <Container maxW="5xl" flex="1" py={8}>
            <Stack spacing={6} h="100%">
              <NicknameGate onNicknameChange={setNickname} />
              <DocumentUploader isDisabled={!isAuthenticated} />
              <Box bg="white" borderRadius="xl" boxShadow="md" p={6} flex="1" display="flex">
                <ChatThread messages={messages} error={error} isLoading={combinedLoading} />
              </Box>
            </Stack>
          </Container>
        </Flex>
        <Box as="footer" borderTopWidth="1px" borderColor="gray.200" bg="white" px={6} py={4}>
          <Container maxW="5xl">
            <MessageComposer
              onSend={sendMessage}
              isLoading={isSending}
              isDisabled={!isAuthenticated || isHistoryLoading}
            />
          </Container>
        </Box>
      </Flex>
    </Flex>
  );
};

export default App;
