<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Event\UserManagement;

use App\Entity\User;
use App\Event\AbstractSystemActionEvent;

class DeleteUserEvent extends AbstractSystemActionEvent
{
    private int $id = 0;

    private ?User $user = null;

    public function getUser(): ?User
    {
        return $this->user;
    }

    public function setUser(?User $user): void
    {
        $this->user = $user;
    }

    /**
     * @return int
     */
    public function getId(): int
    {
        return $this->id;
    }

    /**
     * @param int $id
     */
    public function setId(int $id): void
    {
        $this->id = $id;
    }
}
