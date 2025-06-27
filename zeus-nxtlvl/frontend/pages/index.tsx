import AgentMatrix from '../components/AgentMatrix';
import FloatingChatAI from '../components/FloatingChatAI';
import RunSystemButton from '../components/RunSystemButton';
import TopNavBar from '../components/TopNavBar';
import WalletManager from '../components/WalletManager';

export default function Home() {
  return (
    <div>
      <TopNavBar />
      <AgentMatrix />
      <WalletManager />
      <RunSystemButton />
      <FloatingChatAI />
    </div>
  );
}
