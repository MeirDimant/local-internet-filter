import React, { useEffect, useState } from "react";
import { DragDropContext, Droppable, Draggable } from "react-beautiful-dnd";

const PluginsList: React.FC = () => {
  // State variables to manage the list of request and response plugins
  const [requestPluginsList, setRequestPluginsList] = useState<string[]>([]);
  const [responsePluginsList, setResponsePluginsList] = useState<string[]>([]);

  // Function to handle the drag end event for reordering plugins
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

  // Function to send the new order of plugins to the DB
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

  // Function to handle plugin deletion from the request or the response list
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

  // useEffect hook to fetch the request and response lists when the component mounts
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
        <h1>Plugin List</h1>

        {/* Drag and Drop context for handling drag events */}
        <DragDropContext onDragEnd={handleDragEnd}>
          <div className="droppable-container">

            {/* Droppable area for request plugins */}
            <Droppable droppableId="request-plugins">
              {(provided) => (
                <div>
                  <h3>Request Plugins</h3>
                  <ul
                    className="list"
                    {...provided.droppableProps}
                    ref={provided.innerRef}
                  >
                    {/* List of draggable request plugins */}
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
                            {/* Button to delete the request plugin from the list */}
                            <button
                              className="delete-btn"
                              onClick={() =>
                                handleDeletePlugin(index, "request")
                              }
                            >
                              Delete
                            </button>
                          </li>
                        )}
                      </Draggable>
                    ))}
                    {/* Placeholder for maintaining the space of dragged items */}
                    {provided.placeholder}
                  </ul>
                </div>
              )}
            </Droppable>

            {/* Droppable area for response plugins */}
            <Droppable droppableId="response-plugins">
              {(provided) => (
                <div>
                  <h3>Response Plugins</h3>
                  <ul
                    className="list"
                    {...provided.droppableProps}
                    ref={provided.innerRef}
                  >
                    {/* List of draggable response plugins */}
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
                            {/* Button to delete the response plugin from the list */}
                            <button
                              className="delete-btn"
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
                    {/* Placeholder for maintaining the space of dragged items */}
                    {provided.placeholder}
                  </ul>
                </div>
              )}
            </Droppable>
          </div>
        </DragDropContext>

        {/* Button to send the new order of plugins */}
        <button className="add-btn" onClick={handleSendPluginsList}>
          Send New Order
        </button>
      </div>
    </div>
  );
};

export default PluginsList;
