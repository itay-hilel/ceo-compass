from typing import List, Dict, Any
import json
import logging
import re

logger = logging.getLogger(__name__)

class OrganizationalParser:
    """Handles parsing of organizational communication contexts"""
    
    @staticmethod
    def parse_team_meeting(raw_input: str) -> List[Dict[str, Any]]:
        """Parse team meeting transcripts with role detection"""
        messages = []
        lines = raw_input.split('\n')
        
        for line in lines:
            if ':' in line and not line.startswith('Time:'):
                speaker, content = line.split(':', 1)
                speaker_name = speaker.strip()
                
                # Detect leadership roles
                is_leader = any(title in speaker_name.lower() for title in 
                              ['manager', 'director', 'lead', 'head', 'ceo', 'cto', 'vp'])
                
                messages.append({
                    'speaker': speaker_name,
                    'content': content.strip(),
                    'type': 'meeting_contribution',
                    'is_leadership': is_leader,
                    'word_count': len(content.strip().split()),
                    'has_questions': '?' in content,
                    'has_decisions': any(word in content.lower() for word in 
                                       ['decide', 'decision', 'will do', 'action item'])
                })
        
        return messages
    
    @staticmethod
    def parse_leadership_email(raw_input: str) -> List[Dict[str, Any]]:
        """Parse leadership email threads with hierarchy detection"""
        messages = []
        current_msg = {}
        
        lines = raw_input.split('\n')
        for line in lines:
            if line.startswith('From:'):
                if current_msg:
                    messages.append(current_msg)
                sender = line[5:].strip()
                current_msg = {
                    'speaker': sender,
                    'content': '',
                    'type': 'email',
                    'is_leadership': OrganizationalParser._detect_leadership_email(sender),
                    'urgency_level': 0
                }
            elif line.startswith('Subject:'):
                subject = line[8:].strip()
                current_msg['subject'] = subject
                current_msg['urgency_level'] = OrganizationalParser._assess_urgency(subject)
            elif line.strip() and 'speaker' in current_msg:
                current_msg['content'] += line + '\n'
        
        if current_msg:
            # Final processing
            content = current_msg.get('content', '')
            current_msg.update({
                'word_count': len(content.split()),
                'tone_indicators': OrganizationalParser._detect_tone_indicators(content),
                'has_action_items': any(word in content.lower() for word in 
                                      ['action', 'task', 'deliverable', 'deadline'])
            })
            messages.append(current_msg)
        
        return messages
    
    @staticmethod
    def parse_all_hands(raw_input: str) -> List[Dict[str, Any]]:
        """Parse all-hands/company-wide communications"""
        # Similar to team meeting but with company-wide context
        messages = OrganizationalParser.parse_team_meeting(raw_input)
        
        # Add company-wide specific analysis
        for msg in messages:
            msg['type'] = 'all_hands_contribution'
            msg['visibility'] = 'company_wide'
            
        return messages
    
    @staticmethod
    def parse_slack_channel(raw_input: str) -> List[Dict[str, Any]]:
        """Parse Slack channel conversations"""
        try:
            # Assume JSON format for Slack export
            slack_data = json.loads(raw_input)
            messages = []
            
            for msg in slack_data:
                messages.append({
                    'speaker': msg.get('user', 'unknown'),
                    'content': msg.get('text', ''),
                    'type': 'slack_message',
                    'timestamp': msg.get('ts', ''),
                    'thread_ts': msg.get('thread_ts', ''),
                    'reactions': msg.get('reactions', []),
                    'is_thread_reply': 'thread_ts' in msg and msg.get('thread_ts') != msg.get('ts')
                })
            
            return messages
        except:
            # Fallback to simple parsing
            return OrganizationalParser.parse_team_meeting(raw_input)
    
    @staticmethod
    def auto_detect_communication_type(raw_input: str) -> str:
        """Auto-detect organizational communication type"""
        if 'From:' in raw_input and '@' in raw_input:
            return "leadership_email"
        elif any(keyword in raw_input.lower() for keyword in ['all hands', 'company meeting', 'quarterly']):
            return "all_hands"
        elif 'user' in raw_input and 'ts' in raw_input:
            return "slack_channel"
        else:
            return "team_meeting"
    
    @staticmethod
    def _detect_leadership_email(sender: str) -> bool:
        """Detect if sender is in leadership role"""
        leadership_domains = ['executive', 'ceo', 'cto', 'vp', 'director', 'head']
        return any(title in sender.lower() for title in leadership_domains)
    
    @staticmethod
    def _assess_urgency(subject: str) -> int:
        """Assess email urgency level (0-3)"""
        urgent_keywords = ['urgent', 'asap', 'immediate', 'critical', 'emergency']
        if any(keyword in subject.lower() for keyword in urgent_keywords):
            return 3
        elif any(keyword in subject.lower() for keyword in ['important', 'priority']):
            return 2
        elif any(keyword in subject.lower() for keyword in ['fyi', 'update', 'info']):
            return 1
        return 0
    
    @staticmethod
    def _detect_tone_indicators(content: str) -> List[str]:
        """Detect tone indicators in communication"""
        indicators = []
        
        if any(word in content.lower() for word in ['disappointed', 'concerned', 'frustrated']):
            indicators.append('negative_emotion')
        if any(word in content.lower() for word in ['excited', 'great', 'excellent', 'fantastic']):
            indicators.append('positive_emotion')
        if len([c for c in content if c.isupper()]) / len(content) > 0.1:
            indicators.append('high_intensity')
        if content.count('!') > 2:
            indicators.append('emphatic')
            
        return indicators
    
    @staticmethod
    def extract_team_dynamics(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract team dynamics and organizational metrics"""
        total_messages = len(messages)
        if total_messages == 0:
            return {}
        
        # Leadership participation
        leadership_messages = [m for m in messages if m.get('is_leadership', False)]
        leadership_participation = len(leadership_messages) / total_messages
        
        # Speaking time distribution
        speaker_stats = {}
        for msg in messages:
            speaker = msg.get('speaker', 'unknown')
            if speaker not in speaker_stats:
                speaker_stats[speaker] = {
                    'message_count': 0,
                    'total_words': 0,
                    'questions_asked': 0,
                    'decisions_made': 0,
                    'is_leadership': msg.get('is_leadership', False)
                }
            
            speaker_stats[speaker]['message_count'] += 1
            speaker_stats[speaker]['total_words'] += msg.get('word_count', 0)
            if msg.get('has_questions'):
                speaker_stats[speaker]['questions_asked'] += 1
            if msg.get('has_decisions'):
                speaker_stats[speaker]['decisions_made'] += 1
        
        # Calculate participation balance
        total_words = sum(stats['total_words'] for stats in speaker_stats.values())
        participation_balance = 1.0 - (max(stats['total_words'] for stats in speaker_stats.values()) / total_words) if total_words > 0 else 0
        
        return {
            'total_participants': len(speaker_stats),
            'leadership_participation_rate': leadership_participation,
            'participation_balance': participation_balance,
            'speaker_statistics': speaker_stats,
            'total_questions': sum(msg.get('has_questions', 0) for msg in messages),
            'total_decisions': sum(msg.get('has_decisions', 0) for msg in messages),
            'average_message_length': total_words / total_messages if total_messages > 0 else 0
        }