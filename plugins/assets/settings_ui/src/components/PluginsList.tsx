import React, { useEffect, useState } from "react";
import { DragDropContext, Droppable, Draggable } from "react-beautiful-dnd";

const PluginsList: React.FC = () => {
  const [requestPluginsList, setRequestPluginsList] = useState<string[]>([]);
  const [responsePluginsList, setResponsePluginsList] = useState<string[]>([]);

  const handleDragEnd = (result: any) => {
    const { source, destination } = result;
    if (!destination || source.droppableId !== destination.droppableId) return;

    const isRequestList = source.droppableId.includes("request");
    const list = isRequestList
      ? Array.from(requestPluginsList)
      : Array.from(responsePluginsList);
    const setList = isRequestList
      ? setRequestPluginsList
      : setResponsePluginsList;

    const [reorderedItem] = list.splice(source.index, 1);
    list.splice(destination.index, 0, reorderedItem);

    setList(list);
  };

  const handleSendPluginsList = async () => {
    try {
      await fetch("http://settings.it/api/plugins", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          request_plugins_list: requestPluginsList,
          response_plugins_list: responsePluginsList,
        }),
      });
    } catch (error) {
      console.error("Failed to send new order:", error);
    }
  };

  const handleDeletePlugin = (
    index: number,
    listType: "request" | "response"
  ) => {
    const list =
      listType === "request"
        ? Array.from(requestPluginsList)
        : Array.from(responsePluginsList);
    list.splice(index, 1);
    if (listType === "request") {
      setRequestPluginsList(list);
    } else {
      setResponsePluginsList(list);
    }
  };

  useEffect(() => {
    const fetchPlugins = async () => {
      try {
        const response = await fetch("http://settings.it/api/plugins");
        const data = await response.json();

        const requestData = data.find((item: any) => item.request_plugins_list);
        const responseData = data.find(
          (item: any) => item.response_plugins_list
        );

        setRequestPluginsList(requestData.request_plugins_list);
        setResponsePluginsList(responseData.response_plugins_list);
      } catch (error) {
        console.error("Error fetching contents:", error);
      }
    };

    fetchPlugins();
  }, []);

  return (
    <div className="PluginsList">
      <div className="container">
        <h2>Plugin List</h2>
        <DragDropContext onDragEnd={handleDragEnd}>
          <Droppable droppableId="request-plugins">
            {(provided) => (
              <div>
                <h3>Request Plugins</h3>
                <ul
                  className="list"
                  {...provided.droppableProps}
                  ref={provided.innerRef}
                >
                  {requestPluginsList.map((plugin, index) => (
                    <Draggable
                      key={plugin}
                      draggableId={`request-${plugin}`}
                      index={index}
                    >
                      {(provided) => (
                        <li
                          className="list-item"
                          ref={provided.innerRef}
                          {...provided.draggableProps}
                          {...provided.dragHandleProps}
                        >
                          <h4>{plugin}</h4>
                          <button
                            onClick={() => handleDeletePlugin(index, "request")}
                          >
                            Delete
                          </button>
                        </li>
                      )}
                    </Draggable>
                  ))}
                  {provided.placeholder}
                </ul>
              </div>
            )}
          </Droppable>
          <Droppable droppableId="response-plugins">
            {(provided) => (
              <div>
                <h3>Response Plugins</h3>
                <ul
                  className="list"
                  {...provided.droppableProps}
                  ref={provided.innerRef}
                >
                  {responsePluginsList.map((plugin, index) => (
                    <Draggable
                      key={plugin}
                      draggableId={`response-${plugin}`}
                      index={index}
                    >
                      {(provided) => (
                        <li
                          className="list-item"
                          ref={provided.innerRef}
                          {...provided.draggableProps}
                          {...provided.dragHandleProps}
                        >
                          <h4>{plugin}</h4>
                          <button
                            onClick={() =>
                              handleDeletePlugin(index, "response")
                            }
                          >
                            Delete
                          </button>
                        </li>
                      )}
                    </Draggable>
                  ))}
                  {provided.placeholder}
                </ul>
              </div>
            )}
          </Droppable>
        </DragDropContext>
        <button onClick={handleSendPluginsList}>Send New Order</button>
      </div>
    </div>
  );
};

export default PluginsList;
