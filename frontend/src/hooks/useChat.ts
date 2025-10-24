import { useCallback, useEffect, useMemo, useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { nanoid } from 'nanoid';

import { api } from '../lib/api';
import type {
  ChatCompletionRequest,
  ChatCompletionResponse,
  ChatMessage,
  ConversationDetail,
  ConversationMessage,
} from '../types';

const NICKNAME_KEY = 'flow-nickname';

const toChatMessage = (message: ConversationMessage): ChatMessage => ({
  id: message.id,
  role: message.role,
  content: message.content,
  createdAt: message.created_at,
});

export const useChat = (currentNickname?: string | null) => {
  const queryClient = useQueryClient();
  const [conversationId, setConversationId] = useState<string | undefined>(undefined);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [historyError, setHistoryError] = useState<string | null>(null);
  const [isHistoryLoading, setIsHistoryLoading] = useState(false);

  const nickname = useMemo(() => {
    if (currentNickname) {
      return currentNickname;
    }
    if (typeof window === 'undefined') {
      return undefined;
    }
    return window.localStorage.getItem(NICKNAME_KEY) ?? undefined;
  }, [currentNickname]);

  useEffect(() => {
    if (!nickname) {
      setConversationId(undefined);
      setMessages([]);
      setHistoryError(null);
    }
  }, [nickname]);

  const loadConversation = useCallback(
    async (id: string) => {
      if (!nickname) {
        return;
      }
      setConversationId(id);
      setIsHistoryLoading(true);
      setHistoryError(null);
      try {
        const response = await api.get<ConversationDetail>(`/conversations/${id}`, {
          params: { nickname },
        });
        setMessages(response.data.messages.map(toChatMessage));
      } catch (error) {
        console.error('Failed to load conversation', error);
        setHistoryError('Failed to load conversation history. Please try again.');
      } finally {
        setIsHistoryLoading(false);
      }
    },
    [nickname],
  );

  const mutation = useMutation<
    ChatCompletionResponse,
    Error,
    ChatCompletionRequest,
    { messageId: string }
  >({
    mutationFn: async (payload: ChatCompletionRequest) => {
      const response = await api.post<ChatCompletionResponse>('/chat/completions', payload);
      return response.data;
    },
    onMutate: async (payload: ChatCompletionRequest) => {
      const tempId = nanoid();
      const optimisticMessage: ChatMessage = {
        id: tempId,
        role: 'user',
        content: payload.message,
        createdAt: new Date().toISOString(),
      };
      setMessages((previous) => [...previous, optimisticMessage]);
      return { messageId: tempId };
    },
    onSuccess: async (data: ChatCompletionResponse) => {
      setConversationId(data.conversation_id);
      setMessages(data.messages.map(toChatMessage));
      setHistoryError(null);
      if (nickname) {
        await queryClient.invalidateQueries({ queryKey: ['conversations', nickname] });
      }
    },
    onError: (_error: Error, _variables: ChatCompletionRequest, context) => {
      if (!context?.messageId) {
        return;
      }
      setMessages((previous) => previous.filter((message) => message.id !== context.messageId));
    },
  });

  const sendMessage = useCallback(
    (message: string) => {
      const normalized = message.trim();
      if (!normalized || !nickname) {
        return;
      }
      const payload: ChatCompletionRequest = {
        message: normalized,
        conversation_id: conversationId,
        nickname,
      };
      mutation.mutate(payload);
    },
    [conversationId, mutation, nickname],
  );

  const startNewConversation = useCallback(() => {
    setConversationId(undefined);
    setMessages([]);
    setHistoryError(null);
  }, []);

  const errorMessage = mutation.error?.message ?? historyError ?? undefined;

  return {
    conversationId,
    messages,
    sendMessage,
    selectConversation: loadConversation,
    startNewConversation,
    reset: startNewConversation,
    isLoading: mutation.isPending || isHistoryLoading,
    isSending: mutation.isPending,
    isHistoryLoading,
    error: errorMessage,
  };
};
