import { Box, Container, Stack } from "@chakra-ui/react";
import { useState } from "react";

import { ChatHeader } from "../components/ChatHeader";
import { ChatThread } from "../components/ChatThread";
import { DocumentUploader } from "../components/DocumentUploader";
import { MessageComposer } from "../components/MessageComposer";
import { NicknameGate } from "../components/NicknameGate";
import { useChat } from "../hooks/useChat";

const App = () => {
  const [nickname, setNickname] = useState<string | null>(() => {
    if (typeof window === "undefined") {
      return null;
    }
    return window.localStorage.getItem("flow-nickname");
  });
  const { messages, sendMessage, isLoading, error, reset } = useChat(nickname);
  const isAuthenticated = Boolean(nickname);

  return (
    <Container maxW="5xl" py={10} minH="100vh">
      <Stack spacing={6}>
        <ChatHeader onReset={reset} />
        <NicknameGate onNicknameChange={setNickname} />
        <DocumentUploader isDisabled={!isAuthenticated} />
        <Box bg="white" borderRadius="xl" boxShadow="md" p={6} minH="60vh">
          <ChatThread messages={messages} error={error?.message} isLoading={isLoading} />
        </Box>
        <MessageComposer onSend={sendMessage} isLoading={isLoading} isDisabled={!isAuthenticated} />
      </Stack>
    </Container>
  );
};

export default App;
