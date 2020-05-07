import React, { useState, useContext } from "react";
import { Item, Raid } from "../models";
import { ItemRow } from "./itemRow";
import { groupBy, formatZone } from "../util";
import { ItemSelector } from "./itemSelector";
import { APIItemProvider } from "./itemSelector/itemProvider";
import { APIContext } from "../context";
import {
  maxValidator,
  mcValidator,
  bwlValidator,
  otherValidator,
  PriorityValidatorMessage,
} from "./priorityValidators";

export interface SelectedItemsProps {
  selected: Array<Item>;
  max: number;
  onChangeSelection: (newItems: Array<Item>, isValid: boolean) => void;
  onAddNew: (item: Item, isValid: boolean) => void;
}

export const SelectedItems = (props: SelectedItemsProps) => {
  const groupedSelectedItems = groupBy(props.selected, "zone");
  const api = useContext(APIContext);

  const validators = [
    maxValidator(6),
    mcValidator,
    bwlValidator,
    otherValidator,
  ];

  return (
    <div className="selected-items">
      <div className="selected-items-instructions">
        <span>Priority list rules:</span>
        <ul>
          {validators.map((v) => (
            <li>
              <PriorityValidatorMessage validator={v} items={props.selected} />
            </li>
          ))}
        </ul>
      </div>

      <ItemSelector
        resetOnSelection
        itemProvider={new APIItemProvider(api)}
        onItemSelected={(item: Item) => {
          if (!!props.selected.find((i) => i.id == item.id)) return;

          props.onAddNew(
            item,
            validators.reduce(
              (valid: boolean, validator) =>
                valid && validator.isValid(props.selected.concat(item)),
              true
            )
          );
        }}
      />

      {Object.keys(groupedSelectedItems).map((zone) => {
        return (
          <div className="zone">
            <h2>{formatZone(zone as Raid)}</h2>
            {groupedSelectedItems[zone].map((item) => (
              <ItemRow
                item={item}
                onDelete={() => {
                  const newItems = props.selected.filter(
                    (i) => i.id != item.id
                  );
                  const isValid = validators.reduce(
                    (valid: boolean, validator) =>
                      valid && validator.isValid(newItems),
                    true
                  );

                  props.onChangeSelection(newItems, isValid);
                }}
              />
            ))}
          </div>
        );
      })}
    </div>
  );
};
