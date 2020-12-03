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

export const tierValidator = {
  rule: "Up to  1 item from each tier <a target='_blank' class='tier-link' href='https://docs.google.com/spreadsheets/d/1FbMklpoZPyJFXT4V1797OHIEoyPLk8Z9T3iD_n99VSU/edit#gid=0'>(view tier lists)</a>",
  isValid: (items: Array<Item>) => {
    const tiersSeen = new Map<number, number>();
    items.forEach(i => i.tiers.forEach(t => {
      tiersSeen.set(t.id, (tiersSeen.get(t.id) || 0)+1)
    }))

    return (
      Array.from(tiersSeen.values()).filter(v => v > 1).length == 0
    );
  }
}

export const mcValidator = {
  rule: "Up to 3 items from Molten Core or Onyxia",
  isValid: (items: Array<Item>) => {
    return (
      items.filter((i) => i.zone == Raid.MC || i.zone == Raid.ONY).length <= 3
    );
  },
};

export const bwlValidator = {
  rule: "Up to 3 items from Blackwing Lair",
  isValid: (items: Array<Item>) => {
    return items.filter((i) => i.zone == Raid.BWL).length <= 3;
  },
};

export const aq40Validator = {
  rule: "Up to 3 items from AQ40",
  isValid: (items: Array<Item>) => {
    return items.filter((i) => i.zone == Raid.AQ_40).length <= 3;
  },
};

export const naxxValidator = {
  rule: "Up to 3 items from Naxx",
  isValid: (items: Array<Item>) => {
    return items.filter((i) => i.zone == Raid.NAXX).length <= 3;
  },
}

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
    <span className={valid ? undefined : "invalid"} dangerouslySetInnerHTML={{ __html: props.validator.rule }}></span>
  );
};
