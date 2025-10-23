import {
  Box,
  Button,
  FormControl,
  FormLabel,
  HStack,
  Input,
  Text,
  useToast,
} from "@chakra-ui/react";
import { ChangeEvent, FormEvent, useEffect, useState } from "react";

const NICKNAME_KEY = "flow-nickname";

interface NicknameGateProps {
  onNicknameChange?: (nickname: string | null) => void;
}

export const NicknameGate = ({ onNicknameChange }: NicknameGateProps) => {
  const toast = useToast();
  const [nickname, setNickname] = useState(() => window.localStorage.getItem(NICKNAME_KEY) ?? "");
  const [isEditing, setIsEditing] = useState(!nickname);

  useEffect(() => {
    if (nickname.trim()) {
      const normalized = nickname.trim();
      window.localStorage.setItem(NICKNAME_KEY, normalized);
      onNicknameChange?.(normalized);
    } else {
      window.localStorage.removeItem(NICKNAME_KEY);
      onNicknameChange?.(null);
    }
  }, [nickname, onNicknameChange]);

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!nickname.trim()) {
      toast({ title: "Please choose a nickname", status: "warning", duration: 2000 });
      return;
    }
    setNickname(nickname.trim());
    setIsEditing(false);
    toast({ title: `Welcome, ${nickname}!`, status: "success", duration: 2000 });
  };

  const reset = () => {
    setNickname("");
    setIsEditing(true);
  };

  return (
    <Box bg="white" borderRadius="xl" boxShadow="sm" p={4}>
      {isEditing ? (
        <form onSubmit={handleSubmit}>
          <HStack spacing={3} align="flex-end">
            <FormControl>
              <FormLabel htmlFor="nickname">Nickname</FormLabel>
              <Input
                id="nickname"
                value={nickname}
                onChange={(event: ChangeEvent<HTMLInputElement>) => setNickname(event.target.value)}
                placeholder="Enter a nickname"
              />
            </FormControl>
            <Button type="submit" colorScheme="blue">
              Start chatting
            </Button>
          </HStack>
        </form>
      ) : (
        <HStack justify="space-between">
          <Text color="gray.600">Signed in as {nickname}</Text>
          <Button variant="ghost" onClick={reset}>
            Change nickname
          </Button>
        </HStack>
      )}
    </Box>
  );
};
