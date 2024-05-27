import { useState } from "react";

interface AddDomainFormProps {
  onDomainAdded: () => void;
}

const AddDomainForm: React.FC<AddDomainFormProps> = ({ onDomainAdded }) => {
  const [newDomain, setNewDomain] = useState<string>("");

  const handleAddDomain = async () => {
    try {
      const response = await fetch("http://settings.it/api/approved-domains", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ domain: newDomain }), 
      });
      if (response.ok) {
        setNewDomain(""); 
        onDomainAdded(); 
      }
    } catch (error) {
      console.error("Error adding domain:", error);
    }
  };

  return (
    <div className="add-section">
      <input
        type="text"
        className="add-input"
        value={newDomain}
        onChange={(e) => setNewDomain(e.target.value)}
        placeholder="Add new domain"
      />
      <button className="add-btn" onClick={handleAddDomain}>
        Add
      </button>
    </div>
  );
};

export default AddDomainForm;
