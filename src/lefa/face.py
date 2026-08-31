from typing import Dict, Any

class TheFace:
    """
    The Face: Interface Projection Engine.
    Maps temporal states from The Ark into visual expressions for the frontend character.
    Rule: Must not invent believable fake financial state.
    """
    
    @staticmethod
    def project_state(temporal_state: str, decision: str = None) -> Dict[str, Any]:
        """
        Maps a temporal state to a UI/Character projection.
        OBSERVE (T0) -> LEDGER (T1) -> TIME (T2) -> REVEAL (T3)
        """
        projection = {
            "character_state": "idle",
            "ui_elements": [],
            "message": ""
        }
        
        if temporal_state == "T0":
            projection["character_state"] = "sensing"
            projection["ui_elements"] = ["pulse_ring", "data_stream_readout"]
            projection["message"] = "Observing reality..."
            
        elif temporal_state == "T1":
            if decision == "APPROVE":
                projection["character_state"] = "deliberating_confident"
                projection["message"] = "Policy clears. Synthesizing receipt."
            elif decision == "REJECT":
                projection["character_state"] = "protective_decline"
                projection["message"] = "Risk boundary triggered. Holding."
            else:
                projection["character_state"] = "deliberating"
                
            projection["ui_elements"] = ["ledger_receipt_stamp"]
            
        elif temporal_state == "T2":
            projection["character_state"] = "acting"
            projection["ui_elements"] = ["execution_flash"]
            projection["message"] = "Execution committed to paper boundary."
            
        elif temporal_state == "T3":
            projection["character_state"] = "revealing"
            projection["ui_elements"] = ["temporal_overlay"]
            projection["message"] = "Reality revealed."
            
        else:
            projection["message"] = "Unknown temporal state."
            
        return projection
