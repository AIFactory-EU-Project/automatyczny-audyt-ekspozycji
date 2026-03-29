<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Event\TrainingManagement;

use App\Entity\Training;
use App\Event\AbstractSystemActionEvent;

class UpdateTrainingEvent extends AbstractSystemActionEvent
{
    private ?Training $training = null;

    private int $id = 0;

    public function getId(): int
    {
        return $this->id;
    }

    public function setId(int $id): void
    {
        $this->id = $id;
    }

    public function getTraining(): ?Training
    {
        return $this->training;
    }

    public function setTraining(?Training $training): void
    {
        $this->training = $training;
    }
}
