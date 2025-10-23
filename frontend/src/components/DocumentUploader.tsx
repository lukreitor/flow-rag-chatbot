import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  Progress,
  Stack,
  Text,
  useToast,
} from "@chakra-ui/react";
import { ChangeEvent, useRef, useState } from "react";

import { api } from "../lib/api";

interface DocumentUploaderProps {
  isDisabled?: boolean;
}

export const DocumentUploader = ({ isDisabled = false }: DocumentUploaderProps) => {
  const [isUploading, setIsUploading] = useState(false);
  const inputRef = useRef<HTMLInputElement | null>(null);
  const toast = useToast();

  const handleUpload = async (event: ChangeEvent<HTMLInputElement>) => {
    if (isDisabled) {
      return;
    }
    const file = event.target.files?.[0];
    if (!file) {
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setIsUploading(true);
      await api.post("/documents/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      toast({ title: `${file.name} uploaded`, status: "success", duration: 3000 });
    } catch (error) {
      console.error(error);
      toast({
        title: "Upload failed",
        description: "Please try again or check the file format.",
        status: "error",
      });
    } finally {
      setIsUploading(false);
      event.target.value = "";
    }
  };

  return (
    <Box bg="white" borderRadius="xl" boxShadow="sm" p={4}>
      <Stack spacing={4}>
        <Text fontWeight="semibold">Enhance answers with your own documents</Text>
        <FormControl>
          <FormLabel htmlFor="document">Upload PDF or text (max 10MB)</FormLabel>
          <Input
            ref={inputRef}
            id="document"
            type="file"
            accept=".pdf,.txt,.md"
            onChange={handleUpload}
            display="none"
            isDisabled={isDisabled}
          />
        </FormControl>
        {isUploading ? <Progress size="xs" isIndeterminate /> : null}
        <Button onClick={() => inputRef.current?.click()} isDisabled={isUploading || isDisabled}>
          Upload document
        </Button>
        {!isDisabled ? null : (
          <Text fontSize="sm" color="gray.500">
            Provide a nickname to enable uploads.
          </Text>
        )}
      </Stack>
    </Box>
  );
};
