import React from "react";
import styled from "styled-components";
//import discordIcon from "../images/discord-white.svg";

const ButtonWrap = styled.a`
  display: inline-flex;
  align-items: center;
  padding: 10px 20px 10px 10px;
  font-size: 45px;
  background-color: #7289da;
  border-radius: 5px;
  color: #fff;
  cursor: pointer;
`;
const IconWrap = styled.img`
  height: 80px;
  margin-right: 10px;
`;
const DiscordIcon = () => {
  return null; //return <IconWrap src={discordIcon} alt="discord logo" />;
};

export const DiscordLoginButton = () => (
  <ButtonWrap>
    <DiscordIcon />
    Login with Discord
  </ButtonWrap>
);
