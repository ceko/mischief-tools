import React from "react";
import { Item, ItemTier } from "../models";
import styled from "styled-components";

export interface ItemRowProps {
  item: Item;
  onDelete: () => void;
}

export const ItemRow = (props: ItemRowProps) => {
  return (
    <div className="item-row">
      <ItemTiers tiers={props.item.tiers} />
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

const TierBubble = styled.div<{ color: string }>`
  background-color: ${props => props.color}
`;

export const ItemTiers = (props: { tiers: Array<ItemTier> }) => {
  const { tiers } = props;
  if(tiers?.length) {
    return (
      <div className='tiers'>
        {tiers.map(t => <TierBubble className='tier' color={t.color}>{t.name}</TierBubble>)}
      </div>
    )
  }else{
    return null;
  }
}