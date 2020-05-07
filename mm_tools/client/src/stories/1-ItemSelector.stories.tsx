import React, { useState } from "react";
import { action } from "@storybook/addon-actions";
import { Button } from "@storybook/react/demo";
import { ItemSelector, ItemRow, SelectedItems } from "../components";
import { ItemProvider } from "../components/itemSelector/itemProvider";
import { Raid, Item } from "../models";
import { withKnobs, text, boolean, number } from "@storybook/addon-knobs";

export default {
  title: "Item Selector",
  decorators: [withKnobs],
};

const getItemProvider = (items: number): ItemProvider => {
  return {
    abort: () => {
      console.log("aborting");
    },
    getItems: (filter: string) => {
      console.log("filtering: " + filter);
      return new Promise((resolve, reject) => {
        resolve(
          Array.from({ length: items }, (i: number, v: number) => {
            return {
              id: v,
              name: `Item ${v + 1}`,
              type: "item type",
              slot: "item slot",
              zone: Raid.BWL,
            };
          })
        );
      });
    },
  };
};

export const AutoSuggest = () => (
  <ItemSelector
    itemProvider={getItemProvider(number("Items", 3))}
    onItemSelected={console.log}
  />
);

export const MultipleRows = () => (
  <div style={{ maxWidth: "400px" }}>
    <ItemRow
      item={{
        id: 1,
        name: "item name 2",
        type: "item type",
        slot: "big slot name",
        zone: Raid.BWL,
      }}
      onDelete={console.log}
    />
    <ItemRow
      item={{
        id: 2,
        name: "item name",
        type: "item type",
        slot: "slot name",
        zone: Raid.ONY,
      }}
      onDelete={console.log}
    />
  </div>
);

let cnt = 0;
export const SelectedItemControl = () => {
  const [items, setItems] = useState([] as Array<Item>);

  return (
    <div style={{ maxWidth: "400px" }}>
      <SelectedItems
        selected={items}
        onChangeSelection={setItems}
        max={3}
        onAddNew={() =>
          setItems(
            items.concat({
              id: cnt++,
              name: "Item " + cnt,
              type: "type",
              slot: "slot",
              zone: Raid.BWL,
            })
          )
        }
      />
    </div>
  );
};

const itemCreator = (raid: Raid, total: number) => {
  const items = new Array<Item>();
  for (let i = 0; i < total; i++) {
    items.push({
      id: cnt++,
      name: "item",
      slot: "slot",
      type: "type",
      zone: raid,
    });
  }

  return items;
};

export const SelectedItemControlError = () => {
  const mc_items = number("MC Items", 4);
  const bwl_items = number("BWL Items", 4);
  const ony_items = number("Ony Items", 0);
  const zg_items = number("ZG Items", 0);

  const initialItems = itemCreator(Raid.MC, mc_items)
    .concat(itemCreator(Raid.BWL, bwl_items))
    .concat(itemCreator(Raid.ONY, ony_items))
    .concat(itemCreator(Raid.ZG, zg_items));

  const [items, setItems] = useState([] as Array<Item>);
  if (items.length == 0) {
    setItems(initialItems);
  }

  return (
    <div style={{ maxWidth: "400px" }}>
      <SelectedItems
        selected={items}
        onChangeSelection={setItems}
        max={3}
        onAddNew={() =>
          setItems(
            items.concat({
              id: cnt++,
              name: "Item " + cnt,
              type: "type",
              slot: "slot",
              zone: Raid.BWL,
            })
          )
        }
      />
    </div>
  );
};
