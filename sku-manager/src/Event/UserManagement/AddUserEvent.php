<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Event\UserManagement;

use App\Entity\User;
use App\Event\AbstractSystemActionEvent;

class AddUserEvent extends AbstractSystemActionEvent
{
    private ?User $user = null;

    public function getUser(): ?User
    {
        return $this->user;
    }

    public function setUser(?User $user): void
    {
        $this->user = $user;
    }
}
