<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Event\TrainingManagement;

use App\Entity\Training;
use App\Event\AbstractSystemActionEvent;

class UpdateTrainingValidEvent extends AbstractSystemActionEvent
{
    private ?Training $training = null;

    public function getTraining(): ?Training
    {
        return $this->training;
    }

    public function setTraining(?Training $training): void
    {
        $this->training = $training;
    }
}
