import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { MessageComposer } from "../components/MessageComposer";

describe("MessageComposer", () => {
  it("submits message", () => {
    const onSend = vi.fn();
    render(<MessageComposer onSend={onSend} isLoading={false} />);

    fireEvent.change(screen.getByPlaceholderText(/ask anything/i), { target: { value: "Hello" } });
    fireEvent.click(screen.getByRole("button", { name: /send/i }));

    expect(onSend).toHaveBeenCalledWith("Hello");
  });

  it("does not submit when disabled", () => {
    const onSend = vi.fn();
    render(<MessageComposer onSend={onSend} isLoading={false} isDisabled />);

    fireEvent.change(screen.getByPlaceholderText(/ask anything/i), { target: { value: "Hello" } });
    fireEvent.click(screen.getByRole("button", { name: /send/i }));

    expect(onSend).not.toHaveBeenCalled();
  });
});
