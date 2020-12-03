import React, { useState } from "react";
import { action } from "@storybook/addon-actions";
import { Button } from "@storybook/react/demo";
import { ItemSelector, ItemRow, SelectedItems } from "../components";
import { ItemProvider } from "../components/itemSelector/itemProvider";
import { Raid, Item, ItemTier } from "../models";
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
              tiers: v % 2 == 0 ? [{
                id: 2,
                color: '#FFCCFF',
                name: 'tier 1'
              }] : []
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
        tiers: [{
          id: 2,
          color: '#FFCCFF',
          name: 'tier 1'
        }, {
          id: 3,
          color: '#AABBFF',
          name: 'tier 2'
        }]
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
        tiers: []
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
              tiers: []
            })
          )
        }
      />
    </div>
  );
};

const itemCreator = (raid: Raid, total: number, tiers?: Array<ItemTier>) => {
  const items = new Array<Item>();
  for (let i = 0; i < total; i++) {
    items.push({
      id: cnt++,
      name: "item",
      slot: "slot",
      type: "type",
      zone: raid,
      tiers: tiers || []
    });
  }

  return items;
};

export const SelectedItemControlError = () => {
  const mc_items = number("MC Items", 1);
  const bwl_items = number("BWL Items", 1);
  const ony_items = number("Ony Items", 0);
  const zg_items = number("ZG Items", 0);
  const naxx_items = number("Naxx Items", 4);


  const initialItems = itemCreator(Raid.MC, mc_items)
    .concat(itemCreator(Raid.BWL, bwl_items))
    .concat(itemCreator(Raid.ONY, ony_items))
    .concat(itemCreator(Raid.ZG, zg_items))
    .concat(itemCreator(Raid.NAXX, naxx_items));

  const [items, setItems] = useState([] as Array<Item>);
  if (items.length == 0) {
    setItems(initialItems);
  }

  return (
    <div style={{ maxWidth: "400px" }}>
      <SelectedItems
        key={`${mc_items}-${bwl_items}-${ony_items}-${zg_items}-${naxx_items}`}
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
              tiers: []
            })
          )
        }
      />
    </div>
  );
};


export const TierValidator = () => {
  const t1_items = number("T1 Items", 2);
  const t2_items = number("T2 Items", 2);

  const initialItems = itemCreator(Raid.NAXX, t1_items, [{ id: 1, color: 'red', name: 'red'}])
    .concat(itemCreator(Raid.NAXX, t2_items, [{ id: 2, color: 'green', name: 'green'}]));

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
              tiers: []
            })
          )
        }
      />
    </div>
  );
};