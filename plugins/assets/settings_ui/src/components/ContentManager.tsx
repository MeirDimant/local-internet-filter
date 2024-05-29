import React, { useState } from "react";
import ContentList from "./ContentList";
import AddContentForm from "./AddContentForm";

const ContentManager: React.FC = () => {
  // State variable to manage the refresh key for re-fetching content list
  const [refreshKey, setRefreshKey] = useState<number>(0);

  // Function to handle content changes to re-render the component
  const handleContentChanged = () => {
    setRefreshKey((prevKey) => prevKey + 1);
  };

  return (
    <div className="content-manager">
      <div className="container">
        <ContentList
          refreshKey={refreshKey}
          onContentChanged={handleContentChanged}
        />
        <AddContentForm onContentAdded={handleContentChanged} />
      </div>
    </div>
  );
};

export default ContentManager;
