import React, { useState } from "react";
import ContentList from "./ContentList";
import AddContentForm from "./AddContentForm";

const ContentManager: React.FC = () => {
  const [refreshKey, setRefreshKey] = useState<number>(0);

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
