<?php

namespace App\Entity;

use DateTime;
use Doctrine\ORM\Mapping as ORM;

/**
 * @ORM\Entity(repositoryClass="App\Repository\FailedImportAttemptRepository")
 */
class FailedImportAttempt
{
    /**
     * @ORM\Id()
     * @ORM\GeneratedValue()
     * @ORM\Column(type="integer")
     */
    private $id;

    /**
     * @ORM\Column(type="datetime")
     */
    private $attemptDate;

    /**
     * @ORM\ManyToOne(targetEntity="App\Entity\Camera", inversedBy="photos")
     * @ORM\JoinColumn(name="camera_id", referencedColumnName="id")
     */
    private $camera;

    /**
     * @ORM\Column(type="text", nullable=true)
     */
    private $reason;

    /**
     * @ORM\Column(type="boolean")
     */
    private $retried = false;

    public function __construct()
    {
        $this->attemptDate = new DateTime();
    }

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getAttemptDate(): ?\DateTimeInterface
    {
        return $this->attemptDate;
    }

    public function setAttemptDate(\DateTimeInterface $attemptDate): self
    {
        $this->attemptDate = $attemptDate;

        return $this;
    }

    public function getCamera(): ?Camera
    {
        return $this->camera;
    }

    public function setCamera(Camera $camera): self
    {
        $this->camera = $camera;

        return $this;
    }

    public function getReason(): ?string
    {
        return $this->reason;
    }

    public function setReason(?string $reason): self
    {
        $this->reason = $reason;

        return $this;
    }

    public function getRetried(): ?bool
    {
        return $this->retried;
    }

    public function setRetried(bool $retried): self
    {
        $this->retried = $retried;

        return $this;
    }
}
