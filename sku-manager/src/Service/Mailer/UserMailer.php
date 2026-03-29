<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Service\Mailer;

use App\Entity\User;
use Symfony\Component\DependencyInjection\ParameterBag\ParameterBagInterface;
use Symfony\Component\Mailer\Exception\TransportExceptionInterface;
use Symfony\Component\Mailer\MailerInterface;
use Symfony\Component\Mime\Email;
use Symfony\Component\Security\Core\User\UserInterface;

/**
 * Class RegistrationMailer.
 */
class UserMailer
{
    private MailerInterface $mailer;

    private ParameterBagInterface $parameterBag;

    /**
     * UserMailer constructor.
     *
     * @param MailerInterface       $mailer
     * @param ParameterBagInterface $parameterBag
     */
    public function __construct(MailerInterface $mailer, ParameterBagInterface $parameterBag)
    {
        $this->mailer = $mailer;
        $this->parameterBag = $parameterBag;
    }

    /**
     * @param UserInterface $user
     *
     * @return bool
     *
     * @throws TransportExceptionInterface
     */
    public function sendPasswordChangeMail(UserInterface $user): bool
    {
        if (!$user instanceof User) {
            return false;
        }

        $passwordResetLink = $this->parameterBag->get('frontend_url_password_reset').$user->getConfirmationToken();

        $email = new Email();
        $email->addFrom($this->parameterBag->get('mail_sender_address'));
        $email->subject($this->parameterBag->get('system_name').' - password change request');
        $email->text("Dear user\n\n
Password change request for the ".$user->getEmail()." account has been submitted.\n\n
Please follow this link: {$passwordResetLink} to set your new password.\n\n
Best regards\n
".$this->parameterBag->get('system_name')." Team\n\n
PS. This is an automatic message, in case of any trouble please contact the person responsible for the SKU Manager in your organisation");
        $email->html('<p>Dear user,</p>
<p>Password change request for the '.$user->getEmail()." account has been submitted.</p>
<p>Please follow this link: <a href='{$passwordResetLink}}'>{$passwordResetLink}</a> to set your new password.</p>
<p>Best regards<br>
".$this->parameterBag->get('system_name').' Team</p>
<p>PS. This is an automatic message, in case of any trouble please contact the person responsible for the SKU Manager in your organisation</p>');
        $email->to($user->getEmail());

        $this->mailer->send($email);

        return true;
    }

    /**
     * @param UserInterface $user
     *
     * @return bool
     *
     * @throws TransportExceptionInterface
     */
    public function sendRegistrationMail(UserInterface $user): bool
    {
        if (!$user instanceof User) {
            return false;
        }

        $passwordResetLink = $this->parameterBag->get('frontend_url_password_reset').$user->getConfirmationToken();

        $email = new Email();
        $email->addFrom($this->parameterBag->get('mail_sender_address'));
        $email->subject($this->parameterBag->get('system_name').' - establish password');
        $email->text("Dear user\n\n
Your account ".$user->getEmail().' for the '.$this->parameterBag->get('system_name')." account was prepared for establishing a new password.\n\n
Please follow this link: {$passwordResetLink} to set your new password.\n\n
Best regards\n
".$this->parameterBag->get('system_name')." Team\n\n
PS. This is an automatic message, in case of any trouble please contact the person responsible for the SKU Manager in your organisation");
        $email->html('<p>Dear user,</p>
<p>Your account '.$user->getEmail().' for the '.$this->parameterBag->get('system_name')." account was prepared for establishing a new password.</p>
<p>Please follow this link: <a href='{$passwordResetLink}}'>{$passwordResetLink}</a> to set your new password.</p>
<p>Best regards<br>
".$this->parameterBag->get('system_name').' Team</p>
<p>PS. This is an automatic message, in case of any trouble please contact the person responsible for the SKU Manager in your organisation</p>');
        $email->to($user->getEmail());

        $this->mailer->send($email);

        return true;
    }
}
