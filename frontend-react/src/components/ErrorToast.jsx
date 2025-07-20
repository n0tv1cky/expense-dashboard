import { X } from "lucide-react";
import "./ErrorToast.css";

function ErrorToast({ message, onClose }) {
  return (
    <div className="error-toast">
      <div className="error-content">
        <span className="error-message">{message}</span>
        <button className="error-close" onClick={onClose}>
          <X size={16} />
        </button>
      </div>
    </div>
  );
}

export default ErrorToast;
