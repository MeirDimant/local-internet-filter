import React, { useState, useEffect } from "react";

interface AddContentFormProps {
  onContentAdded: () => void;
}

const AddContentForm: React.FC<AddContentFormProps> = ({ onContentAdded }) => {
  const [domains, setDomains] = useState<string[]>([]);
  const [domainName, setDomainName] = useState("");
  const [content, setContent] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchDomains = async () => {
      setIsLoading(true);
      try {
        const response = await fetch("http://settings.it/api/approved-domains");
        const data: string[] = await response.json();
        setDomains(data);
        if (data.length > 0) {
          setDomainName(data[0]); // Set default domain if list is not empty
        }
        setIsLoading(false);
      } catch (error) {
        console.error("Error fetching approved domains:", error);
        setIsLoading(false);
      }
    };

    fetchDomains();
  }, []);

  const handleAddContent = async () => {
    try {
      const response = await fetch("http://settings.it/api/contents", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ domain_name: domainName, content }),
      });
      if (response.ok) {
        setContent("");
        onContentAdded(); // Refresh content list
      }
    } catch (error) {
      console.error("Error adding content:", error);
    }
  };

  if (isLoading) {
    return <div>Loading...</div>; // Show loading message while fetching
  }

  if (domains.length === 0) {
    return <div>There are no approved domains added.</div>; // Show message if no domains
  }

  return (
    <div className="add-section">
      <select
        className="add-input"
        value={domainName}
        onChange={(e) => setDomainName(e.target.value)}
      >
        {domains.map((domain) => (
          <option key={domain} value={domain}>
            {domain}
          </option>
        ))}
      </select>
      <select
        className="add-input"
        value={content}
        onChange={(e) => setContent(e.target.value)}
      >
        <option value="" disabled selected>
          Please select
        </option>
        <option value="application">Application</option>
        <option value="audio">Audio</option>
        <option value="image">Image</option>
        <option value="multipart">Multipart</option>
        <option value="text">Text</option>
        <option value="video">Video</option>
      </select>
      <button className="add-btn" onClick={handleAddContent}>
        Update allowed content to the chosen domain
      </button>
    </div>
  );
};

export default AddContentForm;
