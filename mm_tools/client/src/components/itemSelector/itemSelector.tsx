import React, {
  FC,
  DetailedHTMLProps,
  ChangeEvent,
  useRef,
  useState,
} from "react";
import { ItemProvider } from "./itemProvider";
import { debounce } from "ts-debounce";
import { Item } from "../../models";
import styled from "styled-components";

type AutoSuggestProps = React.DetailedHTMLProps<
  React.InputHTMLAttributes<HTMLInputElement>,
  HTMLInputElement
>;

class AutoSuggest extends React.Component<
  AutoSuggestProps & {
    onChangeDebounced: (event: ChangeEvent<HTMLInputElement>) => void;
  }
> {
  private onChangeDebounced = debounce(this.props.onChangeDebounced, 300);

  render() {
    return (
      <input
        {...this.props}
        onChange={(event: ChangeEvent<HTMLInputElement>) => {
          event.persist();
          this.props.onChange && this.props.onChange(event);
          this.onChangeDebounced(event);
        }}
      />
    );
  }
}

export interface ItemSelectorProps {
  itemProvider: ItemProvider;
  resetOnSelection?: boolean;
  onItemSelected: (item: Item) => void;
}

interface ItemSelectorState {
  searching: boolean;
  disabled: boolean;
  currentResults: Array<Item>;
  searchText: string;
}

export class ItemSelector extends React.Component<
  ItemSelectorProps,
  ItemSelectorState
> {
  state: ItemSelectorState = {
    disabled: false,
    searching: false,
    currentResults: [],
    searchText: "",
  };
  wrapperRef?: HTMLDivElement;

  componentDidMount() {
    document.addEventListener("mousedown", this.handleClickOutside);
  }

  componentWillUnmount() {
    document.removeEventListener("mousedown", this.handleClickOutside);
  }

  /**
   * Set the wrapper ref
   */
  setWrapperRef = (node: HTMLDivElement) => {
    this.wrapperRef = node;
  };

  /**
   * Alert if clicked on outside of element
   */
  handleClickOutside = (event: any) => {
    if (this.wrapperRef && !this.wrapperRef.contains(event.target)) {
      this.reset();
      this.props.itemProvider.abort();
    }
  };

  onChange = (event: ChangeEvent<HTMLInputElement>) => {
    this.search(event.target.value);
  };

  search = async (filter: string) => {
    this.props.itemProvider.abort();
    if (filter.length < 3) {
      this.setState({
        searching: false,
        disabled: false,
        currentResults: [],
      });
      return;
    }
    this.setState({
      searching: true,
    });
    try {
      this.setState({
        currentResults: await this.props.itemProvider.getItems(filter),
      });
    } finally {
      this.setState({
        searching: false,
        disabled: false,
      });
    }
  };

  reset = () => {
    this.setState({
      currentResults: [],
      searchText: "",
    });
  };

  render() {
    return (
      <div ref={this.setWrapperRef} className="item-selector">
        <AutoSuggest
          value={this.state.searchText}
          className="auto-suggest big"
          placeholder="Search for items..."
          onChange={(event: ChangeEvent<HTMLInputElement>) => {
            this.setState({ disabled: true, searchText: event.target.value });
          }}
          onChangeDebounced={this.onChange}
        />
        {this.state.currentResults.length > 0 && (
          <Results
            disabled={this.state.disabled}
            items={this.state.currentResults}
            onClick={(item) => {
              this.props.onItemSelected(item);
              if (this.props.resetOnSelection) {
                this.reset();
              }
            }}
          />
        )}
      </div>
    );
  }
}

const Result = styled.div`
  cursor: pointer;
  padding: 10px;
  border-bottom: 1px solid #eee;
  &:hover {
    background-color: #eee;
  }
`;

const ResultWrap = styled.div<{ disabled: boolean }>`
  pointerevents: ${(props) => (props.disabled ? "none" : "inherit")};
  ${Result} {
    opacity: ${(props) => (props.disabled ? 0.5 : 1)};
  }
`;

interface ResultsProps {
  items: Array<Item>;
  disabled: boolean;
  onClick: (item: Item) => void;
}

const Results = (props: ResultsProps) => {
  return (
    <ResultWrap className="result-wrap" disabled={props.disabled}>
      {props.items.map((item: Item) => (
        <Result className="result" onClick={() => props.onClick(item)}>
          <div className="name">{item.name}</div>
          <div className="type">{item.type}</div>
          <div className="slot">{item.slot}</div>
        </Result>
      ))}
    </ResultWrap>
  );
};
