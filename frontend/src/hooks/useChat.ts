import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { nanoid } from "nanoid";

import { api } from "../lib/api";
import type { ChatCompletionRequest, ChatCompletionResponse, ChatMessage } from "../types";

const CHAT_HISTORY_KEY = "flow-chat-history";
const CONVERSATION_KEY = "flow-conversation-id";

const loadHistory = (): ChatMessage[] => {
  if (typeof window === "undefined") {
    return [];
  }
  const raw = window.localStorage.getItem(CHAT_HISTORY_KEY);
  if (!raw) {
    return [];
  }
  try {
    return JSON.parse(raw);
  } catch (error) {
    console.error("Failed to parse chat history", error);
    return [];
  }
};

const persistHistory = (messages: ChatMessage[]): void => {
  if (typeof window === "undefined") {
    return;
  }
  window.localStorage.setItem(CHAT_HISTORY_KEY, JSON.stringify(messages));
};

const persistConversationId = (id: string): void => {
  if (typeof window === "undefined") {
    return;
  }
  window.localStorage.setItem(CONVERSATION_KEY, id);
};

const loadConversationId = (): string | undefined => {
  if (typeof window === "undefined") {
    return undefined;
  }
  return window.localStorage.getItem(CONVERSATION_KEY) ?? undefined;
};

export const useChat = (currentNickname?: string | null) => {
  const [conversationId, setConversationId] = useState<string | undefined>(loadConversationId());
  const [messages, setMessages] = useState<ChatMessage[]>(loadHistory);
  const nickname =
    currentNickname ??
    (typeof window !== "undefined"
      ? window.localStorage.getItem("flow-nickname") ?? undefined
      : undefined);

  const mutation = useMutation<ChatCompletionResponse, Error, ChatCompletionRequest, { messageId: string }>({
    mutationFn: async (payload: ChatCompletionRequest) => {
      const response = await api.post<ChatCompletionResponse>("/chat/completions", payload);
      return response.data;
    },
    onMutate: async (payload: ChatCompletionRequest) => {
      const optimisticMessage: ChatMessage = {
        id: nanoid(),
        role: "user",
        content: payload.message,
        createdAt: new Date().toISOString(),
      };
      setMessages((previous: ChatMessage[]) => {
        const next = [...previous, optimisticMessage];
        persistHistory(next);
        return next;
      });
      return { messageId: optimisticMessage.id };
    },
    onSuccess: (data: ChatCompletionResponse) => {
      const newConversationId = data.conversation_id ?? conversationId ?? nanoid();
      setConversationId(newConversationId);
      persistConversationId(newConversationId);

      const assistantMessage: ChatMessage = {
        id: nanoid(),
        role: "assistant",
        content: data.response,
        createdAt: data.created_at,
        sources: data.context,
      };
      setMessages((previous: ChatMessage[]) => {
        const next = [...previous, assistantMessage];
        persistHistory(next);
        return next;
      });
    },
    onError: (_error: Error, _variables: ChatCompletionRequest, context?: { messageId: string }) => {
      if (!context?.messageId) {
        return;
      }
      setMessages((previous: ChatMessage[]) => {
        const next = previous.filter((message: ChatMessage) => message.id !== context.messageId);
        persistHistory(next);
        return next;
      });
    },
  });

  const sendMessage = (message: string) => {
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
  };

  const reset = () => {
    setMessages([]);
    setConversationId(undefined);
    if (typeof window === "undefined") {
      return;
    }
    window.localStorage.removeItem(CHAT_HISTORY_KEY);
    window.localStorage.removeItem(CONVERSATION_KEY);
  };

  return {
    conversationId,
    messages,
    sendMessage,
    reset,
    isLoading: mutation.isPending,
    error: mutation.error,
  };
};
