import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { NicknameGate } from "../components/NicknameGate";

describe("NicknameGate", () => {
  it("stores nickname in local storage", () => {
    const setItemSpy = vi.spyOn(window.localStorage.__proto__, "setItem");
    render(<NicknameGate />);

    fireEvent.change(screen.getByLabelText(/nickname/i), { target: { value: "Alex" } });
    fireEvent.click(screen.getByRole("button", { name: /start chatting/i }));

    expect(setItemSpy).toHaveBeenCalledWith("flow-nickname", "Alex");
  });

  it("notifies parent when nickname changes", () => {
    const onNicknameChange = vi.fn();
    render(<NicknameGate onNicknameChange={onNicknameChange} />);

    fireEvent.change(screen.getByLabelText(/nickname/i), { target: { value: "Taylor" } });
    fireEvent.click(screen.getByRole("button", { name: /start chatting/i }));

    expect(onNicknameChange).toHaveBeenCalledWith("Taylor");
  });
});
