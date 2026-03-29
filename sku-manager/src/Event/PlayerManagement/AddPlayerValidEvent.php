<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Event\PlayerManagement;

use App\Entity\Player;
use App\Event\AbstractSystemActionEvent;

class AddPlayerValidEvent extends AbstractSystemActionEvent
{
    private ?Player $player = null;

    public function getPlayer(): ?Player
    {
        return $this->player;
    }

    public function setPlayer(?Player $player): void
    {
        $this->player = $player;
    }
}
