import React, { useState, useEffect } from "react";
import "./styles/ContentStyle.css";

interface Content {
  domain_name: string;
  content: string[];
}

interface ContentListProps {
  refreshKey: number;
  onContentChanged: () => void;
}

const ContentList: React.FC<ContentListProps> = ({
  refreshKey,
  onContentChanged,
}) => {
  const [contents, setContents] = useState<Content[]>([]);

  useEffect(() => {
    const fetchContents = async () => {
      try {
        const response = await fetch("http://settings.it/api/contents");
        const data: Content[] = await response.json();
        setContents(data);
      } catch (error) {
        console.error("Error fetching contents:", error);
      }
    };

    fetchContents();
  }, [refreshKey]);

  const handleDelete = async (domainName: string, content: string) => {
    try {
      await fetch("http://settings.it/api/contents", {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ domain_name: domainName, content }),
      });
      onContentChanged();
    } catch (error) {
      console.error("Error deleting content:", error);
    }
  };

  return (
    <div>
      <h1>Content List</h1>
      <ul className="list">
        {contents.map(({ domain_name, content }) => (
          <li key={domain_name} className="list-item">
            <strong>{domain_name}</strong>
            <ul className="horizontal-list">
              {content.sort().map((item, index) => (
                <li
                  onDoubleClick={() => handleDelete(domain_name, item)}
                  key={index}
                >
                  {item}
                </li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ContentList;
