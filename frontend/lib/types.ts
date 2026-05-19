export type User = {
  id: string;
  email: string;
  name: string;
  is_platform_admin: boolean;
};

export type AuthResponse = {
  access_token: string;
  token_type: string;
  user: User;
  workspace_id: string;
};

export type Site = {
  id: string;
  workspace_id: string;
  site_key: string;
  name: string;
  domain?: string | null;
  allowed_domains: string[];
  widget_color: string;
  widget_position: string;
  welcome_message: string;
  offline_message: string;
  ai_enabled: boolean;
  human_chat_enabled: boolean;
  show_branding: boolean;
  status: string;
  created_at: string;
  updated_at: string;
};

export type Visitor = {
  id: string;
  site_id: string;
  visitor_uid: string;
  browser?: string | null;
  os?: string | null;
  device_type?: string | null;
  language?: string | null;
  last_seen_at: string;
  is_online: boolean;
};

export type Conversation = {
  id: string;
  site_id: string;
  visitor_id: string;
  assigned_agent_id?: string | null;
  status: string;
  channel: string;
  started_at: string;
  last_message_at?: string | null;
};

export type Message = {
  id: string;
  conversation_id: string;
  sender_type: string;
  sender_user_id?: string | null;
  content: string;
  created_at: string;
};

export type Knowledge = {
  id: string;
  site_id: string;
  title: string;
  content: string;
  category?: string | null;
  is_active: boolean;
};

export type Lead = {
  id: string;
  site_id: string;
  name?: string | null;
  email?: string | null;
  phone?: string | null;
  telegram?: string | null;
  whatsapp?: string | null;
  message?: string | null;
  source_url?: string | null;
  status: string;
  created_at: string;
};

export type Plan = {
  id: string;
  name: string;
  price_monthly?: string | null;
  max_sites?: number | null;
  max_agents?: number | null;
  max_ai_messages_monthly?: number | null;
  allow_remove_branding: boolean;
  allow_custom_color: boolean;
};
