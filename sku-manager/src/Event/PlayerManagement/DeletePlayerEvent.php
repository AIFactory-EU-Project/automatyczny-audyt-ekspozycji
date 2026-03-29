<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Event\PlayerManagement;

use App\Entity\Player;
use App\Event\AbstractSystemActionEvent;

class DeletePlayerEvent extends AbstractSystemActionEvent
{
    private ?Player $player = null;

    private int $id = 0;

    public function getId(): int
    {
        return $this->id;
    }

    public function setId(int $id): void
    {
        $this->id = $id;
    }

    public function getPlayer(): ?Player
    {
        return $this->player;
    }

    public function setPlayer(?Player $player): void
    {
        $this->player = $player;
    }
}
