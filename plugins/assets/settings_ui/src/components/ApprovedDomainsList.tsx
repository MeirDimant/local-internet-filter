import { useState, useEffect } from "react";

interface ApprovedDomainsListProps {
  refreshKey: number;
}

const ApprovedDomainsList: React.FC<ApprovedDomainsListProps> = ({
  refreshKey,
}) => {
  // State variable to store the list of approved domains
  const [domains, setDomains] = useState<string[]>([]);

  // Function to fetch the list of approved domains
  const fetchDomains = async () => {
    try {
      const response = await fetch("http://settings.it/api/approved-domains");
      const data: string[] = await response.json();
      setDomains(data); // Update the state with the fetched domains
    } catch (error) {
      console.error("Error fetching approved domains:", error);
    }
  };

  // useEffect hook to fetch the domains whenever the refreshKey changes
  useEffect(() => {
    fetchDomains();
  }, [refreshKey]);

  // Function to handle domain deletion
  const handleDelete = (domain: string) => {
    fetch("http://settings.it/api/approved-domains", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ domain }),
    })
      .then((response) => response.json())
      .then((data) => setDomains(data)); // Update the state with the new list of domains after deletion
  };

  return (
    <div>
      <h1>Approved Domains</h1>
      {/* List of approved domains with delete buttons */}
      <ul className="list">
        {domains.map((domain) => (
          <li key={domain} className="list-item">
            {domain}
            <button className="delete-btn" onClick={() => handleDelete(domain)}>
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ApprovedDomainsList;
