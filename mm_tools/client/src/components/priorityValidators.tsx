import React from "react";
import { Item, Raid } from "../models";

export interface ItemValidator {
  rule: string;
  isValid: (items: Array<Item>) => boolean;
}

export const maxValidator = (max: number) => {
  return {
    rule: `Up to ${max} items total`,
    isValid: (items: Array<Item>) => {
      return items.length <= max;
    },
  };
};

export const mcValidator = {
  rule: "Up to 3 items from Molten Core",
  isValid: (items: Array<Item>) => {
    return items.filter((i) => i.zone == Raid.MC).length <= 3;
  },
};

export const bwlValidator = {
  rule: "Up to 3 items from Blackwing Lair",
  isValid: (items: Array<Item>) => {
    return items.filter((i) => i.zone == Raid.BWL).length <= 3;
  },
};

export const otherValidator = {
  rule: "Optional: Fill remaining slots with other raids",
  isValid: (items: Array<Item>) => {
    return true;
  },
};

export const PriorityValidatorMessage = (props: {
  validator: ItemValidator;
  items: Array<Item>;
}) => {
  const valid = props.validator.isValid(props.items);
  return (
    <span className={valid ? undefined : "invalid"}>
      {props.validator.rule}
    </span>
  );
};
