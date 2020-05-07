import React, { useContext, FC } from "react";
import { APIContext } from "../context";
import { API } from "../api";
import { Item } from "../models";
import { SelectedItems } from "../components";

export const PriorityManagementPage: FC = () => {
  const api = useContext(APIContext);

  return <Page api={api} />;
};

interface PageProps {
  api: API;
}

enum SetupState {
  None,
  Fetching,
  Success,
  Error,
}

interface PageState {
  setupState: SetupState;
  priority: Array<Item>;
  saveEnabled: boolean;
  saveButtonText: string;
}

class Page extends React.Component<PageProps, PageState> {
  state = {
    setupState: SetupState.None,
    priority: [],
    saveEnabled: false,
    saveButtonText: "Save Changes",
  } as PageState;

  private feelGood: HTMLDivElement | null = null;
  componentDidMount() {
    this.setup();
  }

  setup = async () => {
    this.setState({
      setupState: SetupState.Fetching,
    });
    const { api } = this.props;

    try {
      const priorityPage = await api.getPriority();
      this.setState({
        priority: priorityPage.results.map((pi) => pi.item),
        setupState: SetupState.Success,
      });
    } catch {
      this.setState({
        setupState: SetupState.Error,
      });
    }
  };

  private isFetching = () => this.state.setupState == SetupState.Fetching;
  private isError = () => this.state.setupState == SetupState.Error;
  private isSuccess = () => this.state.setupState == SetupState.Success;

  addNewItem = (item: Item, isValid: boolean) => {
    if (!!this.state.priority.find((i) => i.id == item.id)) return;

    this.setState({
      priority: this.state.priority.concat(item),
      saveEnabled: isValid,
    });
  };

  private saveButtonTimeout?: number;
  setSaveButton = (text: string) => {
    clearTimeout(this.saveButtonTimeout);
    this.setState({
      saveButtonText: text,
    });

    this.saveButtonTimeout = setTimeout(() => {
      this.setState({
        saveButtonText: "Save Changes",
      });
    }, 3000);
  };

  save = async () => {
    if (!this.state.saveEnabled) return;

    try {
      await this.props.api.updatePriority(this.state.priority.map((i) => i.id));
      this.setSaveButton("Save Successful!");
      if (this.feelGood) {
        this.feelGood.classList.add("feel-good-animate");
        setTimeout(() => {
          this.feelGood!.classList.remove("feel-good-animate");
        }, 4000);
      }
    } catch {
      this.setSaveButton("Error Saving :(");
    }
  };

  render() {
    return (
      <div>
        <h1>Priority Management</h1>

        {this.isFetching() && <div>Fetching priority...</div>}
        {this.isError() && (
          <div>Error getting priority items. Try to refresh the page.</div>
        )}
        {this.isSuccess() && (
          <div className="selected-item-wrap">
            <SelectedItems
              max={6}
              selected={this.state.priority}
              onAddNew={this.addNewItem}
              onChangeSelection={(newSelections, isValid) =>
                this.setState({ priority: newSelections, saveEnabled: isValid })
              }
            />
            <div className="spacer"></div>
            <div
              className={
                "button save-prio big centered " +
                (this.state.saveEnabled ? "" : "disabled")
              }
              onClick={this.save}
            >
              {this.state.saveButtonText}
            </div>
          </div>
        )}
        <div ref={(el) => (this.feelGood = el)} className="feels-good"></div>
      </div>
    );
  }
}
