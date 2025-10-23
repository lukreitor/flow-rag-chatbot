export type Role = "user" | "assistant";

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
}

export interface ChatCompletionRequest {
  message: string;
  conversation_id?: string;
  nickname: string;
}
