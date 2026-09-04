import { Sparkles, CircleCheck } from "lucide-react";

function Header() {
  return (
    <header className="header">
      <div className="brand">
        <div className="brand-icon">
          <Sparkles size={20} />
        </div>

        <div>
          <h1>EarningsInsight</h1>
          <p>AI-Powered Earnings Intelligence</p>
        </div>
      </div>
    </header>
  );
}

export default Header;