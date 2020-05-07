import React from "react";
import { Item } from "../models";

export interface ItemRowProps {
  item: Item;
  onDelete: () => void;
}

export const ItemRow = (props: ItemRowProps) => {
  return (
    <div className="item-row">
      <div className="name">{props.item.name}</div>
      <div className="type">{props.item.type}</div>

      <div className="item-action">
        <div className="button delete" onClick={props.onDelete}>
          delete
        </div>
      </div>
    </div>
  );
};
