import React from "react";
import { action } from "@storybook/addon-actions";
import { Button } from "@storybook/react/demo";
import { DiscordLoginButton } from "../components";

export default {
  title: "Buttons",
  component: DiscordLoginButton,
};

export const DiscordLogin = () => <DiscordLoginButton />;
