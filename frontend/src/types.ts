export type Role = 'user' | 'assistant';

export interface DocumentContext {
  document_id: string;
  score: number;
  content: string;
}

export interface ChatMessage {
  id: string;
  role: Role;
  content: string;
  createdAt: string;
  sources?: DocumentContext[];
}

export interface ChatCompletionResponse {
  conversation_id: string;
  response: string;
  context: DocumentContext[];
  created_at: string;
  messages: ConversationMessage[];
}

export interface ChatCompletionRequest {
  message: string;
  conversation_id?: string;
  nickname: string;
}

export interface ConversationMessage {
  id: string;
  role: Role;
  content: string;
  created_at: string;
}

export interface ConversationSummary {
  id: string;
  nickname: string;
  title: string | null;
  created_at: string;
  updated_at: string;
  last_message_preview?: string | null;
}

export interface ConversationDetail extends ConversationSummary {
  messages: ConversationMessage[];
}
